<template>
  <header>
    <nav>
      <span class="brand">🎵 Songs</span>
      <router-link to="/" data-cy="home-cypress-test">Home</router-link>
      <router-link to="/log-in" data-cy="login-cypress-test">Log-In</router-link>
      <router-link to="/log-out">Log-Out</router-link>
      <router-link to="/faq">FAQ</router-link>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; }
header { background: #2d3436; padding: 14px 30px; }
nav { display: flex; align-items: center; gap: 24px; }
nav .brand { color: #00b894; font-size: 1.3rem; font-weight: bold; margin-right: auto; }
nav a { color: #dfe6e9; text-decoration: none; font-size: 0.9rem; padding: 6px 12px; border-radius: 4px; transition: background 0.2s; }
nav a:hover { background: #636e72; }
main { max-width: 960px; margin: 40px auto; padding: 0 24px; }
</style>