import styled from 'styled-components';
import { Outlet, Link } from "react-router-dom";

const Nav = styled.nav` 
font-size: 18px;
position: sticky;
top: 0;
z-index: 999;
height: 80px;
background-color: rgba(0, 0, 0, 0.5);
/* box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.5); */
box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.15);
display: flex;
justify-content: left;
align-items: center;
`;


const Layout = () => {
  return (
    <>
      <Nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/CS241">CS241</Link>
          </li>
          <li>
            <Link to="/CS410">CS410</Link>
          </li>
          <li>
            <Link to="/test">test</Link>
          </li>
          <li>
            <Link to="/TopicsCS410">Topics CS410</Link>
          </li>
          <li>
            <Link to="/Timeline">Timeline</Link>
          </li>
        </ul>
      </Nav>

      <Outlet />
    </>
  )
};

export default Layout;