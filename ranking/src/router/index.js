import Vue from 'vue'
import Router from 'vue-router'

// Containers
const DefaultContainer = () => import('@/DefaultContainer');

// Views
const Dashboard = () => import('@/components/HelloWorld');
const Profile = () => import('@/components/Profile');

Vue.use(Router);

const router = new Router({
  mode: 'history', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'open active',
  scrollBehavior: () => ({y: 0}),

  routes: [
    {
      path: '/',
      redirect: '/dashboard',
      name: 'Home',
      component: DefaultContainer,
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard
        },
        {
          path: 'profile/:id',
          name: 'Profile',
          component: Profile,
          props: true,
        },
      ]
    },
    // {
    //   path: '*',
    //   name: 'Page404',
    //   component: Page404
    // },
  ]
});



export default router
