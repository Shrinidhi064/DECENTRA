const ChequeMetadata = artifacts.require("ChequeMetadata");
const ModelCIDStorage = artifacts.require("ModelCIDStorage");
const SignatureRegistry=artifacts.require("SignatureRegistry");
const ChequeMetadatanew=artifacts.require("ChequeMetadatanew");

module.exports = function (deployer) {
  deployer.deploy(ChequeMetadata);
  deployer.deploy(ModelCIDStorage);
  deployer.deploy(SignatureRegistry);
  deployer.deploy(ChequeMetadatanew);
};
