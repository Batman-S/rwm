import { WebSocketProvider } from "./contexts/WebSocketContext";
import "./ui/css/tailwind.css";
import Layout from "./components/Common/Layout";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { RecoilRoot } from "recoil";
import WaitlistForm from "./components/WaitlistForm";
import CheckIn from "./components/CheckIn";
import Completed from "./components/Completed";

function App() {
  return (
    <Router>
      <RecoilRoot>
        <WebSocketProvider>
          <Layout>
            <Routes>
              <Route path="/" element={<WaitlistForm />} />
              <Route path="/check-in" element={<CheckIn />} />
              <Route path="/completed" element={<Completed />} />
            </Routes>
          </Layout>
        </WebSocketProvider>
      </RecoilRoot>
    </Router>
  );
}

export default App;
