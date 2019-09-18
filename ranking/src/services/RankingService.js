import Api from '@/services/Api'

export default {
  fetchRankings () {
    return Api().get('user')
  },
  getUser (params) {
    return Api().get('user/' + params.id)
  },
  addUser (params) {
    return Api().post('user', params)
  },
  updateUser (params) {
    return Api().put('user/' + params.username, params)
  },

  deleteUser (id) {
    return Api().delete('user/' + id)
  }
}
