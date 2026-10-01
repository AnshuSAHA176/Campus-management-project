import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter } from "react-router-dom";
import StudentContext from "./context/StudentContext.jsx";
import TeacherContext from "./context/TeacherContext.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <TeacherContext>
      <StudentContext>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </StudentContext>
    </TeacherContext>
  </StrictMode>,
);
