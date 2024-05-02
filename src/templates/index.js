{% comment %} const routes = {
  '/': {
    linkLabel: 'Home',
    content: `I am in home page`
  },
  '/signup': {
    linkLabel: 'Signup',
    content: `I am in signup page`
  },
  '/login': {
    linkLabel: 'Login',
    content: `I am in login page`,
  },
};

const app = document.querySelector('.cover-container-sd');
const nav = document.querySelector('.navbar-nav');

const renderNavLinks = () => {
  Object.keys(routes).forEach(route => {
    const { linkLabel } = routes[route];
    const linkElement = document.createElement('a');
    linkElement.href = route;
    linkElement.textContent = linkLabel;
    linkElement.className = 'nav-link';
    nav.appendChild(linkElement);
  });
};

const renderContent = route => {
  app.innerHTML = routes[route].content;
};

const navigate = e => {
  e.preventDefault();
  const route = new URL(e.target.href).pathname;
  history.pushState({}, "", route);
  renderContent(route);
};

const registerNavLinks = () => {
  nav.addEventListener('click', navigate);
};

const renderInitialPage = () => {
  const route = location.pathname;
  renderContent(route);
};

const registerBrowserBackAndForth = () => {
  window.onpopstate = function (e) {
    const route = location.pathname;
    renderContent(route);
  };
};

// Call functions to initialize
renderInitialPage();
renderNavLinks();
registerNavLinks();
registerBrowserBackAndForth(); {% endcomment %}
