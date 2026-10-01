import { useContext, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useFormik } from "formik";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";

import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

import { teacherDataContext } from "../context/TeacherContext";
import axios from "axios";

export default function TeacherLogin() {
  const [showPassword, setShowPassword] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);
  const [error, setError] = useState(false);

  const navigate = useNavigate();

  const { setTeacher } = useContext(teacherDataContext);

  // Validation
  const validate = (values) => {
    const errors = {};

    // Email validation
    if (!values.email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email)) {
      errors.email = "Please enter a valid email";
    }

    // Password validation
    if (!values.password) {
      errors.password = "Password is required";
    } else if (values.password.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    return errors;
  };

  // Formik
  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },

    validate,

    onSubmit: async (values) => {
      setError(false);

      const teacherData = {
        email: values.email,
        password: values.password,
      };

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BASE_URL}/login/`,
          teacherData,
        );

        if (response.status === 200) {
          setTeacher(response.data);

          localStorage.setItem("accessToken", response.data.access);

          localStorage.setItem("refreshToken", response.data.refresh);

          localStorage.setItem("role", response.data.role);

          navigate("/teacher-profile");
        }
      } catch (err) {
        if (err.response?.status === 400) {
          setError(true);
        }
      }
    },
  });

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <div className="w-full max-w-2xl mx-auto px-8 sm:px-10 pt-12 sm:pt-28">
        <div className="mb-10">
          <h1 className="text-4xl sm:text-6xl font-medium tracking-tight text-white">
            Teacher Login
          </h1>
        </div>

        <form onSubmit={formik.handleSubmit}>
          <div className="mb-7">
            <label
              htmlFor="email"
              className="block mb-2 text-lg text-neutral-300"
            >
              Email Address
            </label>

            <TextField
              id="email"
              name="email"
              type="email"
              fullWidth
              placeholder="example@gmail.com"
              value={formik.values.email}
              onChange={(e) => {
                formik.handleChange(e);
                setError(false);
              }}
              onBlur={formik.handleBlur}
              error={formik.touched.email && Boolean(formik.errors.email)}
              helperText={formik.touched.email && formik.errors.email}
              sx={{
                "& .MuiOutlinedInput-root": {
                  backgroundColor: "#050505",
                  borderRadius: "12px",
                  color: "#fff",

                  "& fieldset": {
                    borderColor: "#292929",
                  },

                  "&:hover fieldset": {
                    borderColor: "#444",
                  },

                  "&.Mui-focused fieldset": {
                    borderColor: "#E85A24",
                  },
                },

                "& .MuiInputBase-input": {
                  padding: "16px",
                  fontSize: "18px",
                  color: "#fff",

                  "&::placeholder": {
                    color: "#666",
                    opacity: 1,
                  },
                },

                "& .MuiFormHelperText-root": {
                  marginLeft: 0,
                },
              }}
            />
          </div>

          {/* Password */}
          <div className="mb-10">
            <label
              htmlFor="password"
              className="block mb-2 text-lg text-neutral-300"
            >
              Password
            </label>

            <TextField
              id="password"
              name="password"
              fullWidth
              type={showPassword ? "text" : "password"}
              placeholder="Enter your password here"
              value={formik.values.password}
              onChange={(e) => {
                formik.handleChange(e);
                setError(false);
              }}
              onBlur={(e) => {
                formik.handleBlur(e);
                setPasswordFocused(false);
              }}
              onFocus={() => setPasswordFocused(true)}
              error={formik.touched.password && Boolean(formik.errors.password)}
              helperText={formik.touched.password && formik.errors.password}
              slotProps={{
                input: {
                  endAdornment: passwordFocused ? (
                    <InputAdornment position="end">
                      <IconButton
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => setShowPassword((prev) => !prev)}
                        edge="end"
                        sx={{
                          color: "#777",

                          "&:hover": {
                            color: "#E85A24",
                          },
                        }}
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ) : null,
                },
              }}
              sx={{
                "& .MuiOutlinedInput-root": {
                  backgroundColor: "#050505",
                  borderRadius: "12px",
                  color: "#fff",

                  "& fieldset": {
                    borderColor: "#292929",
                  },

                  "&:hover fieldset": {
                    borderColor: "#444",
                  },

                  "&.Mui-focused fieldset": {
                    borderColor: "#E85A24",
                  },
                },

                "& .MuiInputBase-input": {
                  padding: "16px",
                  fontSize: "18px",
                  color: "#fff",

                  "&::placeholder": {
                    color: "#666",
                    opacity: 1,
                  },
                },

                "& .MuiFormHelperText-root": {
                  marginLeft: 0,
                },
              }}
            />
          </div>

          {error && (
            <div className="mb-5">
              <p className="text-red-500 text-sm">
                Incorrect email or password. Please try again.
              </p>
            </div>
          )}

          <div className="mb-8">
            <Button
              type="submit"
              variant="contained"
              fullWidth
              sx={{
                background: "linear-gradient(to right, #E85A24, #9b2b05)",
                borderRadius: "12px",
                padding: "12px",
                fontSize: "18px",
                fontWeight: 500,
                textTransform: "none",

                "&:hover": {
                  background: "linear-gradient(to right, #F0642B, #C8471A)",
                },
              }}
            >
              Log In
            </Button>
          </div>

          <p className="text-center text-lg text-neutral-500">
            New here?{" "}
            <Link
              to="/student-register"
              className="text-[#E85A24] hover:text-[#FF6B32] transition-colors"
            >
              Register as a Student
            </Link>
          </p>
        </form>
      </div>

      <div className="mt-auto py-8">
        <p className="text-center text-sm text-neutral-600">
          Powered by Anshu & Mrinmoy
        </p>
      </div>
    </div>
  );
}
