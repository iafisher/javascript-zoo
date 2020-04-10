'use strict';

module.exports = {
  up: (queryInterface, Sequelize) => {
    return queryInterface.bulkInsert('Projects', [{
      name: 'default',
      slug: 'default',
      description: 'Lorem ipsum',
      archived: false,
      // Sequelize creates this field for you automatically but doesn't populate it.
      // Incredible.
      createdAt: new Date().toDateString(),
      updatedAt: new Date().toDateString(),
    }], {});
  },

  down: (queryInterface, Sequelize) => {
    return queryInterface.bulkDelete('Projects', null, {});
  }
};
