import Layout from "./pages/Layout";
import Error from "./pages/Error";
import Forecast from "./pages/Forecast";
import Dashboard from "./pages/Dashboard";
import { createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <Error />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "forecast",
        element: <Forecast />,
      },
    ],
  },
]);

export default router;
