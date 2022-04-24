#!/usr/bin/env perl 
use strict;
use warnings;

=pod

Populates the C<docker-compose.yml> file with services from the C<services/> directory,
expecting them to be defined as C<category/name> with a C<config.yml>
there will be a Redis cluster along with PostgreSQL cluster for every category.
In config there are some rquired

- language:

As for every language C<base/language/> settigs will be included.

=cut

use Template;
use Path::Tiny;
use YAML::XS qw(LoadFile);
use Dotenv;
use Syntax::Keyword::Try;

use Log::Any qw($log);
use Log::Any::Adapter qw(Stderr), log_level => 'info';

my %TYPES = (
    perl    => [ 'pm', 'pl', 'perl', 'ff' ],
    rust    => [ 'rs', 'rust' ],
    python  => [ 'py', 'python' ],
    nodejs  => [ 'js', 'nodejs' ],
);

my %default_env = (
    REDIS_CLUSTER      => "1",
    LOG_LEVEL          => "info",
);

my $env;
try {
    $env = Dotenv->parse('bin/.env');
} catch ($e) {
    $log->warnf('Could not load main .env file (bin/.env) | %s', $e);
}

my $service_dir = path('services');
my @cat_dirs = grep { $_->is_dir } $service_dir->children;
my ( @services, @categories );
for my $category (@cat_dirs) {
    # per category
    my $cat_env;
    try {
        $cat_env = Dotenv->parse($category->child('.env')->stringify);
    } catch ($e) {
        $log->warnf('Could not load category %s env file | %s', $category, $e);
    }
    push @categories, {name => $category->basename, env => $cat_env};

    # Services
    for my $srv (grep { $_->is_dir } $category->children) {
        my $config_path = $srv->child('config.yml');
        my $config;
        my $cat_name = $category->basename;
        try {
            $config = LoadFile($srv->child('config.yml'));
        } catch ($e) {
            $log->warnf('Service config does not exist %s | %s', $srv, $e);
        }
        my %args;
        my $path = join '/', 'services', $category->basename, $srv->basename;
        my @service_dir = $srv->child('lib/Service/')->children;
        my ($service_name, $type) = $service_dir[0] =~ /.*\/(.*)\.(.*)/m;
        my $lang;
        ($lang) = grep { grep { /$type|$config->{language}/ } $TYPES{$_}->@* } keys %TYPES;

        # Image
        if($srv->child('Dockerfile')->exists) {
            $args{build}{dockerfile} = join '/', $path, 'Dockerfile';
        } else {
            $args{build}->{dockerfile} = join '/', 'base', $lang, 'Dockerfile';
            $args{build}->{context} = './';
            $args{build}->{args}{base_dir} = join '/', 'base', $lang;
            # perl specific
            $args{build}->{args}{service_dir} = $path if $srv->child('cpanfile')->exists || $srv->child('aptfile')->exists;
        }
        
        # At the moment only one Service should be present.
        $args{environment}{SERVICE_NAME} = "Service::$service_name";
        $args{environment}{APP}          = $cat_name;
        $args{environment}{DATABASE}     = "postgresql://$cat_name-pg-0";
        $args{environment}{REDIS}        = "redis://$cat_name-redis-node-0:6379";
        $args{environment}{SERVICE_DIR}  = '/app/';

        # Include additional environment variables.
        @{$args{environment}}{keys %default_env} = values %default_env;
        my $env_file = $srv->child('.env');
        if ( $env_file->is_file ) {
            my $env = Dotenv->parse($env_file->stringify);
            @{$args{environment}}{keys %$env} = values %$env;
        }


        $args{volumes} = ["./$path:/app/", './pg_service.conf:/root/.pg_service.conf:ro'];
        if ($config->{port}) {
            $args{ports} = [$config->{port}.':'.$config->{port}];
        }
        if($config->{instances}) {
            push @services, {
                %args,
                instance => join('_', $category->basename, $srv->basename, $_),
                name     => $srv->basename,
                category => $category->basename,
            } for sort keys +($config->{instances} || {})->%*;
        } else {
            push @services, {
                %args,
                instance => join('_', $category->basename, $srv->basename),
                name     => $srv->basename,
                category => $category->basename,
            }
        }
    }
}


$log->tracef('- %s', $_) for @services;
$log->infof('%d total categories defined', 0 + @categories);
$log->infof('%d total services defined', 0 + @services);

my $tt = Template->new;
$tt->process(
    'templates/docker-compose.yml.tt2',
    {
        service_list => \@services,
        category_list => \@categories,
        env => $env,
    },
    'docker-compose.yml'
) or die $tt->error;

