/* eslint-disable node/no-unpublished-require */
const path = require('path');
const gulp = require('gulp');
const log = require('fancy-log');
const del = require('del');
const sass = require('gulp-sass');
const postcss = require('gulp-postcss');
const sourcemaps = require('gulp-sourcemaps');
const imagemin = require('gulp-imagemin');

const debug = process.env.NODE_ENV !== 'production';

const paths = {
  clean: 'dude/static/**/*',
  styles: {
    src: ['src/scss/**/*.scss'],
    dest: 'dude/static/css/',
  },
  scripts: {
    src: ['src/ts/**/*.ts'],
    dest: 'dude/static/js/',
  },
  images: {
    src: ['assets/img/**/*'],
    dest: 'dude/static/img/',
  },
  webfonts: {
    src: ['node_modules/@fortawesome/fontawesome-pro/webfonts/**/*'],
    dest: 'dude/static/webfonts',
  },
};

const cleanFiles = function cleanFiles() {
  return del([paths.clean])
    .then(files => {
      for (const f of files)
        log('Cleaned "%s".', path.relative('.', f));

      log('Cleaned %d paths.', files.length);
    });
};

const shrinkImages = function shrinkImages() {
  let stream = gulp.src(paths.images.src);

  if (!debug)
    stream = stream.pipe(imagemin());

  stream = stream.pipe(gulp.dest(paths.images.dest));
  return stream;
};

const transpileSass = function transpileSass() {
  const postcssPlugins = [
    require('precss'),
    require('autoprefixer'),
  ];
  if (!debug)
    postcssPlugins.push(require('cssnano'));

  return gulp.src(paths.styles.src)
    .pipe(sourcemaps.init())
    .pipe(sass({ includePaths: ['node_modules'] })
      .on('error', log.error))
    .pipe(postcss(postcssPlugins))
    .pipe(sourcemaps.write('.', { includeContent: !debug }))
    .pipe(gulp.dest(paths.styles.dest));
};

const copyWebfonts = function copyWebfonts() {
  return gulp.src(paths.webfonts.src)
    .pipe(gulp.dest(paths.webfonts.dest));
};

const build = gulp.series(
  cleanFiles,
  gulp.parallel(
    shrinkImages,
    transpileSass,
    copyWebfonts,
  ),
);

module.exports = exports = {
  build,
  clean: cleanFiles,
  cleanFiles,
  copyWebfonts,
  default: build,
  imagemin: shrinkImages,
  shrinkImages,
  transpileSass,
};
