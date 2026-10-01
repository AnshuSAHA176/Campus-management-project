import React, { createContext, useState } from "react";

export const teacherDataContext = createContext();

export default function TeacherContext({ children }) {
  const [teacher, setTeacher] = useState(null);
  return (
    <div>
      <teacherDataContext.Provider value={{ teacher, setTeacher }}>
        {children}
      </teacherDataContext.Provider>
    </div>
  );
}
