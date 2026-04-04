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
      path: '/character-search',
      name: 'character-search',
      component: () => import('../views/CharacterSearchView.vue'),
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
  ],
})

export default router
