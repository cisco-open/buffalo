import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '13a'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '46f'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '600'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '064'),
            routes: [
              {
                path: '/docs/category/getting-started',
                component: ComponentCreator('/docs/category/getting-started', '01f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/Getting-started/Architecture',
                component: ComponentCreator('/docs/Getting-started/Architecture', 'a67'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/Getting-started/Contributing',
                component: ComponentCreator('/docs/Getting-started/Contributing', '138'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/Getting-started/Installation',
                component: ComponentCreator('/docs/Getting-started/Installation', '9d8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/Getting-started/Usage',
                component: ComponentCreator('/docs/Getting-started/Usage', 'da0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/Getting-started/why-buffalo',
                component: ComponentCreator('/docs/Getting-started/why-buffalo', 'b82'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '889'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
