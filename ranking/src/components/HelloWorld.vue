<template>
  <div class="hello">
    <b-card class="mb-2" v-for="user in users">
      <b-img style="float:left" src="https://picsum.photos/125/125/?image=58" width="75" height="75" rounded="circle" alt="Circle image"></b-img>
      <div style="float:left" class="ml-3">
        <h4 class="mt-1"> <router-link :to="{ name: 'Profile', params: { id: user._id } }"> {{user.fullName}}</router-link></h4>
        45th President of the United States of America
      </div>
   </b-card>
  </div>
</template>

<script>
  import rankingService from '../services/RankingService.js'
  export default {
    data: () => {
      return {
        users: [],
      }
    },
    beforeCreate() {
      rankingService.fetchRankings().then(response => {
        this.users = response.data.posts
        console.log(response.data.posts)
      }).catch(error => {
        console.log("error")
      });

      // rankingService.addUser({username: 'willsned',
      // fullName: "William Snedegar",
      // instaScore: 0,
      // twitterHandle: "yeetboi",}).then(response => {
      //   console.log(response.data)
      // }).catch(error => {
      //   console.log("error")
      // });
    },
    methods: {

    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
