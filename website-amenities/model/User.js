const mongoose = require("mongoose");

const UserSchema = mongoose.Schema({
  username: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  },
  password: {
    type: String,
    required: true
  },
  properties: [{type:mongoose.Schema.Types.ObjectId, ref: 'property'}]
});

module.exports = mongoose.model("user", UserSchema);