import ChatInterface from './components/chat-interface.js';

// Get Vue from window since it's loaded via CDN
const { createApp, ref } = window.Vue;
const { Quasar } = window;

// Vue App Configuration
const app = createApp({
  setup() {
    return {
      drawerLeft: ref(false),
      drawerRight: ref(true)
    };
  },
  components: {
    ChatInterface
  }
});

// Configure Quasar and Mount the App
app.use(Quasar, {
  config: {
    brand: {
      primary: '#1976D2',
      secondary: '#26A69A',
      accent: '#9C27B0',
      dark: '#1D1D1D',
    },
  }
});

app.mount('#app');
