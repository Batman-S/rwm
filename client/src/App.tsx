import { WebSocketHandler } from "./socket/WebSocketHandler";
import "./ui/css/tailwind.css";
import Layout from "./components/Common/Layout";
import { BrowserRouter as Router } from "react-router-dom";

import AppRoutes from "./routes/AppRoutes";

function App() {
  return (
    <Router>
      <WebSocketHandler />
      <Layout>
        <AppRoutes />
      </Layout>
    </Router>
  );
}

export default App;
