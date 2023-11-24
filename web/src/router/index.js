import {createRouter, createWebHistory} from 'vue-router'
import SuperIndexView from "@/views/SuperIndexView";

const routes = [
  {
    path:"/",
    name:"home",
    redirect:"/super",
  },
  {
    path:"/super",
    name:"super_home",
    component: SuperIndexView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to,from,next)=>{
//   if(to.meta.requestAuth&&!store.state.user.is_login){
//     next({name:"user_account_login", query:{toPage:to.name}});
//   } else {
//     next();
//   }
// })

export default router