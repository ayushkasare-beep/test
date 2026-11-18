const Contract = artifacts.require('Addition');
module.exports = function (deployer) {
  deployer.deploy(Contract);
};
