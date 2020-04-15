'use strict';
module.exports = (sequelize, DataTypes) => {
  const Task = sequelize.define('Task', {
    shortDescription: DataTypes.STRING,
    longDescription: DataTypes.STRING,
    order: DataTypes.INTEGER,
    status: DataTypes.STRING
  }, {});
  Task.associate = function(models) {
    models.Task.belongsTo(models.Project, {
      foreignKey: 'projectId',
      onDelete: 'SET NULL',
      allowNull: true,
    });
    models.Task.belongsTo(models.Task, {
      foreignKey: 'parentId',
      onDelete: 'SET NULL',
      allowNull: true,
    });
  };
  return Task;
};
