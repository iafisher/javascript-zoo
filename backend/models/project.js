'use strict';
module.exports = (sequelize, DataTypes) => {
  const Project = sequelize.define('Project', {
    name: DataTypes.STRING,
    slug: DataTypes.STRING,
    description: DataTypes.STRING,
    archived: DataTypes.BOOLEAN
  }, {});
  Project.associate = function(models) {
    // associations can be defined here
  };
  return Project;
};