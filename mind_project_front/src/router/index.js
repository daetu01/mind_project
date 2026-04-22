import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }

    return {
      top: 0,
      behavior: 'smooth',
    }
  },
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/raid-rankings',
      name: 'raid-rankings',
      component: () => import('../views/RaidRankingsView.vue'),
    },
    {
      path: '/matching',
      name: 'matching',
      component: () => import('../views/MatchingView.vue'),
    },
    {
      path: '/lfg',
      name: 'lfg',
      component: () => import('../views/LfgBoardView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/CharacterProfileView.vue'),
    },
    {
      path: '/queue',
      name: 'queue',
      component: () => import('../views/QueueDashboardView.vue'),
    },
    {
      path: '/guild/:name',
      name: 'guild-detail',
      component: () => import('../views/GuildDetailView.vue'),
    },
  ],
})

export default router
