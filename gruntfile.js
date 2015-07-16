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
                    'ckanext/wprdc/public/assets/css/<%= pkg.domain %>.css': 'scss/main.scss'
                }
            }
        },

        sync: {
            main: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: [
                            'bower_components/foundation/js/foundation.min.js',
                            'bower_components/foundation/js/vendor/modernizr.js'
                        ],
                        dest: 'ckanext/wprdc/public/assets/js'
                    }
                ],
                verbose: true
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

    grunt.registerTask('default', ['sync','sass','watch']);
    grunt.registerTask('build', ['sync','sass']);
};