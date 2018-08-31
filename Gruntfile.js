'use strict';
const path = require('path');
// "grunt-cssurlrev": "^1.0.1",

module.exports = function (grunt) {
  const buildDest = 'dude/static/';

  const gruntConfig = {
    pkg: grunt.file.readJSON('package.json'),

    availabletasks: {
      tasks: {},
    },

    clean: {
      default: {
        dot: true,
        src: [
          path.join(buildDest, '**', '*'),
          '!' + path.join(buildDest, '.gitignore'),
        ],
      }
    },

    postcss: {
      options: {
        syntax: require('postcss-scss'),
        processors: [
          require('@csstools/postcss-sass')({
            includePaths: ['node_modules'],
          }),
          require('pixrem')(),
          require('autoprefixer')(),
          require('postcss-preset-env')(),
          require('cssnano')(),
        ],
      },
      default: {
        expand: true,
        cwd: 'src/scss/',
        src: ['**/*.scss'],
        dest: path.join(buildDest, 'css'),
        ext: '.css',
      },
    },

    ts: {
      default: {
        tsconfig: 'tsconfig.json',
        expand: true,
        cwd: 'src/ts/',
        src: ['**/*.ts'],
        dest: path.join(buildDest, 'js'),
      },
    },

    browserify: {
      options: {
        browserifyOptions: {
          paths: [
            './node_modules/',
          ],
        },
        plugin: [
          'tsify',
        ],
        transform: [
          [
            'babelify', {
              presets: ['@babel/preset-env'],
              exts: ['.js', '.ts'],
            },
          ],
          [
            'uglifyify', {
              exts: ['.js', '.ts'],
            },
          ],
        ],
      },
      default: {
        src: ['src/js/*.js', 'src/ts/*.ts'],
        dest: path.join(buildDest, 'js', 'bundle.js'),
      },
    },

    uglify: {
      default: {
        expand: true,
        cwd: 'dude/static/js/',
        src: ['**/*.js', '!**.min.js'],
        dest: 'dude/static/js/',
        ext: '.min.js',
      }
    },

    copy: {
      webfonts: {
        expand: true,
        cwd: 'node_modules/@fortawesome/fontawesome-pro/webfonts/',
        src: ['**/*'],
        dest: 'dude/static/webfonts/',
      },
    },

    imagemin: {
      options: {
        optimizationLevel: 3,
      },
      default: {
        expand: true,
        cwd: 'src/img/',
        src: '**/*',
        dest: 'dude/static/img/',
      },
    },

    cachebuster: {
      default: {
        options: {
          basedir: 'dude/static/',
          format: 'json',
          compilerOptions: {
            rootDir: 'src/ts/',
          },
        },
        src: ['dude/static/**/*', '!dude/static/manifest.json'],
        dest: 'dude/static/manifest.json',
      },
    },
  };

  grunt.initConfig(gruntConfig);
  require('load-grunt-tasks')(grunt);

  grunt.registerTask('default', ['availabletasks']);

  grunt.registerTask('build', [
    'clean',
    'postcss',
    'ts',
    'browserify',
    'uglify',
    'copy',
    'imagemin',
  ]);
};
