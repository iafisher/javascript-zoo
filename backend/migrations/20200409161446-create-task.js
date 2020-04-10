'use strict';
module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.createTable('Tasks', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      shortDescription: {
        type: Sequelize.STRING
      },
      longDescription: {
        type: Sequelize.STRING
      },
      order: {
        type: Sequelize.INTEGER
      },
      status: {
        type: Sequelize.STRING
      },
      projectId: {
        type: Sequelize.INTEGER,
        onDelete: "SET NULL",
        allowNull: true,
        references: {
          model: 'Projects',
          key: 'id',
        }
      },
      parentId: {
        type: Sequelize.INTEGER,
        onDelete: "SET NULL",
        allowNull: true,
        references: {
          model: 'Tasks',
          key: 'id',
        }
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  down: (queryInterface, Sequelize) => {
    return queryInterface.dropTable('Tasks');
  }
};
