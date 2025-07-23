module.exports = {
  // The devServer object is the one that will be passed to webpack-dev-server
  devServer: (devServerConfig, { env, paths, proxy, allowedHost }) => {
    // This is the fix for the CORS error.
    // It tells the development server to proxy any request starting with /api
    // to your backend server at http://localhost:5001
    devServerConfig.proxy = {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      },
    };

    /* 
      This is where you can override the devServer configuration.
      The 'devServerConfig' object is the original config from react-scripts.
      We are replacing the deprecated middleware hooks with the new `setupMiddlewares`.
    */
    devServerConfig.setupMiddlewares = (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      // This is where you could add custom middleware.
      // For example, to add a mock API endpoint before other routes:
      // This logic runs before the webpack-dev-middleware.
      devServer.app.get('/api/hello', (req, res) => {
        res.json({ message: 'Hello from custom middleware!' });
      });

      // It's important to return the middlewares array.
      return middlewares;
    };

    // It's important to return the modified config.
    return devServerConfig;
  },
};