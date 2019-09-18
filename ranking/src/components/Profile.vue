<template>
  <div>
    <div class="row">
      <div class="col-4" style="text-align:center">
        <b-img src="https://picsum.photos/125/125/?image=58" height="100%" rounded="circle" alt="Circle image"></b-img>
      </div>
      <div class="col-8">
        <h5>{{user.fullName}}</h5>

        <div>
          Instagram Username: {{user.username}} <br>
          Twitter Handle: {{user.twitterHandle}} <br>
          InstaScore: {{user.instaScore}}

      </div>
      </div>
    </div>
  </div>

</template>

<script>
import rankingService from '../services/RankingService.js'

export default {
  name: 'Profile',
  props: ["id"],
  data() {
    return {
      user: {},
    }
  },
  created() {
    rankingService.getUser({id:this.id}).then(response => {
      this.user = response.data
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

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
