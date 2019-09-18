var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var UserSchema = new Schema({
  username: String,
  fullName: String,
  instaScore: Number,
  twitterHandle: String,
},{ collection: 'instaUsers' });

var User = mongoose.model("User", UserSchema);
module.exports = User;
