import { Outlet, createRootRoute } from "@tanstack/react-router"
import React, { Suspense } from "react"

import NotFound from "../components/Common/NotFound"
import { Route as Home } from './home';

const loadDevtools = () =>
  Promise.all([
    import("@tanstack/router-devtools"),
    import("@tanstack/react-query-devtools"),
  ]).then(([routerDevtools, reactQueryDevtools]) => {
    return {
      default: () => (
        <>
          <routerDevtools.TanStackRouterDevtools />
          <reactQueryDevtools.ReactQueryDevtools />
        </>
      ),
    }
  })

const TanStackDevtools =
  process.env.NODE_ENV === "production" ? () => null : React.lazy(loadDevtools)

// routes/__root.tsx
export const Route = createRootRoute({
    component: () => (
      <>
        <Outlet /> {/* 자식 라우트를 렌더링 */}
        <Suspense>
          <TanStackDevtools />
        </Suspense>
      </>
    ),
    notFoundComponent: () => <NotFound />, // 404 페이지 구성
  });
  
  export const routeTree = Route.addChildren([
    Home, // "/" 라우트를 설정
  ]);