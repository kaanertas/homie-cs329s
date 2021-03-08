const mongoose = require("mongoose");
const MONGOURI = "mongodb+srv://pujan:pujanpatel@cs329s.gefiw.mongodb.net/cs329s?retryWrites=true&w=majority";

const InitiateMongoServer = async () => {
  try {
    await mongoose.connect(MONGOURI, {
      useNewUrlParser: true
    });
    console.log("Successfully connected to the database!!");
  } catch (e) {
    console.log(e);
    throw e;
  }
};

module.exports = InitiateMongoServer;