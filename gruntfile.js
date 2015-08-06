module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        sass: {
            options: {
                outputStyle: 'compressed',
                includePaths: ['bower_components/foundation/scss']
            },
            dist: {
                files: {
                    'ckanext/wprdc/fanstatic/styles/<%= pkg.domain %>.css': 'scss/main.scss'
                }
            }
        },

        clean: {
          js: ['ckanext/wprdc/fanstatic/scripts/vendor/*.min.js']
        },

        sync: {
            min: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: [
                            'bower_components/foundation/js/foundation.min.js',
                            'bower_components/foundation/js/vendor/modernizr.js'
                        ],
                        dest: 'ckanext/wprdc/fanstatic/scripts/vendor'
                    }
                ]
            },
            rename_foundation: {
                src: 'ckanext/wprdc/fanstatic/scripts/vendor/foundation.min.js',
                dest: 'ckanext/wprdc/fanstatic/scripts/vendor/foundation.js'
            }
        },

        watch: {
            sass: {
                files: ['scss/**/*.scss','bower_components/foundation/scss/**/*.scss'],
                tasks: ['sass']
            }
        }
    });

    require('load-grunt-tasks')(grunt, { scope: 'devDependencies' });
    require('time-grunt')(grunt);

    grunt.registerTask('default', ['sync', 'clean', 'sass','watch']);
    grunt.registerTask('build', ['sync', 'clean', 'sass']);
};