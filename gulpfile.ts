import del from 'del';
import {
  dest,
  parallel,
  series,
  src,
  TaskFunction
  } from 'gulp';
import autoprefixer from 'gulp-autoprefixer';
import copy from 'gulp-copy';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';
import path from 'path';
import buffer from 'vinyl-buffer';

// transpile typescript into javascript
// bundle javascript
// uglify javascript
// transpile scss into css
// autoprefixer css
// minify css

const maxInt = 2 ** 32 - 1;
const getRandomIntInclusive = (min = 0, max = maxInt) => {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
};
const getRandomWait = () => getRandomIntInclusive(5, 30) * 1000;


const root = path.resolve(__dirname);
const assets = path.join(root, 'assets');
const modules = path.join(root, 'node_modules');
const destRoot = path.join(root, 'dude', 'static', 'build');
const sassSuffix = path.join('scss', '**', '*.scss');

const cleanPaths = [
  path.join(destRoot, '*'),
  '!' + path.join(destRoot, '.gitkeep'),
];

const fontawesome = path.join(modules, '@fortawesome', 'fontawesome-pro');

const sassPaths = [
  path.join(assets, sassSuffix),
  path.join(fontawesome, sassSuffix),
  path.join(modules, 'bootstrap', sassSuffix),
];


export const clean: TaskFunction = () => {
  return del(cleanPaths);
};

export const cssTranspile: TaskFunction = () => {
  return src(sassPaths)
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false,
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(dest(path.join(destRoot, 'css')));
};

const cssMinify: TaskFunction = cb => {
  setTimeout(cb, getRandomWait());
};

const jsTranspile: TaskFunction = cb => {
  setTimeout(cb, getRandomWait());
};

const jsBundle: TaskFunction = cb => {
  setTimeout(cb, getRandomWait());
};

const jsMinify: TaskFunction = cb => {
  setTimeout(cb, getRandomWait());
};

export const publish: TaskFunction = () => {
  const paths = [
    path.join(fontawesome, 'webfonts', '*'),
  ];

  return src(paths)
    .pipe(buffer())
    .pipe(copy(destRoot, {prefix: 3}))
    .pipe(dest(destRoot));
};

export const build = series(
  clean,
  parallel(
    cssTranspile,
    series(jsTranspile, jsBundle)
  ),
  parallel(cssMinify, jsMinify),
  publish
);
