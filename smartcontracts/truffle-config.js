module.exports = {
  networks: {
      development: {
          host: "127.0.0.1",
          port: 7545, // or whichever port Ganache is using
          network_id: "*"
      }
  },
  compilers: {
      solc: {
          version: "0.8.19" // Match this with your contract's Solidity version
      }
  }
};
