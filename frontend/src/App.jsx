import React from "react";
import { Route, Routes } from "react-router-dom";
import LandingPage from "./components/LandingPage.jsx";
import StudentLogin from "./features/auth/pages/StudentLogin.jsx";
import StudentRegister from "./features/auth/pages/StudentRegister.jsx";
import TeacherLogin from "./features/auth/pages/TeacherLogin.jsx";
import StudentDashboard from "./features/student/pages/StudentDashboard.jsx";
import TeacherDashboard from "./features/teacher/pages/TeacherDashboard.jsx";
import StudentLogout from "./features/auth/pages/StudentLogout.jsx";
import TeacherLogout from "./features/auth/pages/TeacherLogout.jsx";
import StudentProtectWrapper from "./features/auth/guards/StudentProtectWrapper.jsx";
import TeacherProtectWrapper from "./features/auth/guards/TeacherProtectWrapper.jsx";
import StudentProfileSetup from "./features/student/pages/StudentProfileSetup.jsx";
import TeacherProfileSetup from "./features/teacher/pages/TeacherProfileSetup.jsx";

import CampusMapPage from "./features/campus-map/pages/CampusMapPage.jsx";

export default function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/student-login" element={<StudentLogin />} />
        <Route path="/teacher-login" element={<TeacherLogin />} />
        <Route path="/student-register" element={<StudentRegister />} />
        <Route
          path="/student/dashboard"
          element={
            <StudentProtectWrapper>
              <StudentDashboard />
            </StudentProtectWrapper>
          }
        />
        <Route
          path="/teacher/dashboard"
          element={
            <TeacherProtectWrapper>
              <TeacherDashboard />
            </TeacherProtectWrapper>
          }
        />

        <Route
          path="/student-profile-setup"
          element={
            <StudentProtectWrapper>
              <StudentProfileSetup />
            </StudentProtectWrapper>
          }
        />

        <Route
          path="/teacher-profile-setup"
          element={
            <TeacherProtectWrapper>
              <TeacherProfileSetup />
            </TeacherProtectWrapper>
          }
        />

          <Route 
          path="/campus-map"
          element={<CampusMapPage/>}
          
          />

        <Route
          path="/student/logout"
          element={
            <StudentProtectWrapper>
              <StudentLogout />
            </StudentProtectWrapper>
          }
        />
        <Route
          path="/teacher/logout"
          element={
            <TeacherProtectWrapper>
              <TeacherLogout />
            </TeacherProtectWrapper>
          }
        />
      </Routes>
    </div>
  );
}
