const mongoose = require("mongoose");

const MisclassifiedSchema = mongoose.Schema({
  false_positives: {
    type: [String],
    required: true
  },
  false_negatives: {
    type: [String],
    required: true
  },
  property: {
    type: mongoose.Schema.Types.ObjectId, 
    ref: 'property',
    required: true
  },
});

module.exports = mongoose.model("misclassified", MisclassifiedSchema);