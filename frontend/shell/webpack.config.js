// webpack.config.js for Shell App (port 3000)

const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const ModuleFederationPlugin = require("webpack/lib/container/ModuleFederationPlugin");
const webpack = require("webpack");

module.exports = {
  mode: "development",
  entry: "./src/index.jsx",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist"),
    publicPath: "http://localhost:3000/",
  },
  resolve: {
    extensions: [".js", ".jsx"],
    fallback: {
      process: require.resolve("process/browser"),
      buffer: require.resolve("buffer"),
    },
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        use: "babel-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  plugins: [
    new webpack.ProvidePlugin({
      process: "process/browser",
      Buffer: ["buffer", "Buffer"],
    }),
    new HtmlWebpackPlugin({
      template: "./public/index.html",
    }),
    new ModuleFederationPlugin({
      name: "shell",
      remotes: {
        supportTicketsApp:
          "supportTicketsApp@http://localhost:3001/remoteEntry.js", // Use localhost for development
      },
      shared: {
        react: {
          singleton: true,
          requiredVersion: "^17.0.2",
          eager: false, // Change to false
        },
        "react-dom": {
          singleton: true,
          requiredVersion: "^17.0.2",
          eager: false, // Change to false
        },
      },
    }),
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, "dist"),
    },
    compress: true,
    port: 3000,
    host: "0.0.0.0",
    historyApiFallback: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
};
