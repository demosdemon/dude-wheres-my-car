import path from 'path';
import webpack from 'webpack';

const sourceMap = true;

const debug = process.env.NODE_ENV !== 'production';
const publicHost = debug ? 'http://localhost:2992' : '';

const assetsPath = path.join(__dirname, 'assets');

const _loader = function (loader: string, options?: { [key: string]: any }): webpack.RuleSetLoader {
  options = options || {};
  if (!Object.prototype.hasOwnProperty.call(options, 'sourceMap'))
    options.sourceMap = sourceMap;

  return { loader, options };
};

const config: webpack.Configuration = {
  context: __dirname,
  entry: {
    main: './assets/js/main',
    layout: path.join(assetsPath, 'scss', 'style.scss'),
  },
  mode: debug ? 'development' : 'production',
  module: {
    rules: [
      {
        test: /\.s?css$/,
        use: [
          _loader('style-loader'),
          _loader('css-loader', { module: true }),
          _loader('resolve-url-loader'),
          _loader('sass-loader'),
        ],
      }, {
        test: /\.(eot|svg|ttf|woff2?)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[hash].[ext]',
              outputPath: 'fonts/'
            }
          }
        ]
      },
    ],
  },
  output: {
    chunkFilename: '[id].[hash].js',
    filename: '[name].[hash].js',
    path: path.join(__dirname, 'dude', 'static', 'build'),
    publicPath: `${publicHost}/static/build`,
  },
};

export default config;
