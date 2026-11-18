const Contract = artifacts.require('Prime');
module.exports = function (deployer) {
  deployer.deploy(Contract);
};
