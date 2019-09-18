const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const morgan = require('morgan')
const app = express()
app.use(morgan('combined'))
app.use(bodyParser.json())
app.use(cors())

var User = require("../models/user");
var mongoose = require('mongoose');

mongoose.connect('mongodb+srv://willsned:Cardinals1@cluster0-lcapt.gcp.mongodb.net/test?retryWrites=true&w=majority', {useNewUrlParser: true, dbName: 'pymongo_test'});
var db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error"));
db.once("open", function(callback){
  console.log("Connection Succeeded");
});

// Add new post
app.post('/user', (req, res) => {
  var db = req.db;
  var new_post = new User({
    username: req.body.username,
    fullName: req.body.fullName,
    instaScore: req.body.instaScore,
    twitterHandle: req.body.twitterHandle
  })

  new_post.save(function (error) {
    if (error) {
      console.log(error)
    }
    res.send({
      success: true,
      message: 'Post saved successfully!'
    })
  })
})

app.get('/user', (req, res) => {
  User.find({}, function (error, posts) {
    console.log(posts);
    if (error) { console.error(error); }
    res.send({
      posts: posts
    })
  }).sort({instaScore:-1})
})

app.get('/user/:id', (req, res) => {
  var db = req.db;
  User.findById(req.params.id, function (error, post) {
    console.log(post);
    if (error) { console.error(error); }
    res.send(post)
  })
})

// Update a post
app.put('/user/:id', (req, res) => {
  var db = req.db;
  User.findById(req.params.id, function (error, post) {
    if (error) { console.error(error); }

    post.username= req.body.username,
    post.fullName= req.body.fullName,
    post.twitterHandle= req.body.twitterHandle
    post.save(function (error) {
      if (error) {
        console.log(error)
      }
      res.send({
        success: true
      })
    })
  })
})

app.delete('/user/:id', (req, res) => {
  var db = req.db;
  User.remove({
    _id: req.params.id
  }, function(err, post){
    if (err)
      res.send(err)
    res.send({
      success: true
    })
  })
})

app.listen(process.env.PORT || 8081)
