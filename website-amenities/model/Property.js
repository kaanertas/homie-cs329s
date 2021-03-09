const mongoose = require("mongoose");

const PropertySchema = mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  photo_urls: {
    type: [String],
    required: true
  },
  labeled_photo_urls: {
    type: [String],
    required: true
  },
  model_pred_labels: {
    type: [String],
    required: true
  },
  labels: {
    type: [String],
    required: true
  },
});

module.exports = mongoose.model("property", PropertySchema);