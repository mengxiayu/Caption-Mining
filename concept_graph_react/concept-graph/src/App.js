import {
  BrowserRouter as Router,
  Routes,
  Route,
  // Link
} from "react-router-dom";

import logo from './logo.svg';
import './App.css';
import Layout from './pages/Layout';
import { ForceGraph } from './components/force_graph_svg';

import data from './data/course_concepts.json';
// import data from './graph_data/contexts';



function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
      </header>

      <div>
        <nav className='Nav'>
          <Router>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<Home />} />
                {/* <Route path="users" element={<Users />} />
                <Route path="about" element={<About />} /> */}
              </Route>
            </Routes>
          </Router>
        </nav>

        <ForceGraph
          nodesData={data}
          nodeHoverTooltip={0} />


      </div>
    </div>
  );
}


function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Users() {
  return <h2>Users</h2>;
}

export default App;
