const Shipping = artifacts.require("Shipping");
const truffleAssert = require('truffle-assertions');

module.exports = function (deployer) {
  deployer.deploy(Shipping);
};