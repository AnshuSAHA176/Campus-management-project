import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useFormik } from "formik";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";

import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

import { studentDataContext } from "../context/StudentContext";
import axios from "axios";

export default function StudentRegister() {
  const [showPassword, setShowPassword] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);
  const [error, setError] = useState(false);

  const navigate = useNavigate();

  const { setStudent } = useContext(studentDataContext);

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

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },

    validate,

    onSubmit: async (values) => {
      setError(false);

      const newStudent = {
        email: values.email,
        password: values.password,
        role: "student",
      };

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BASE_URL}/register/`,
          newStudent,
        );

        if (response.status === 201) {
          setStudent(response.data);

          const loginResponse = await axios.post(
            `${import.meta.env.VITE_BASE_URL}/login/`,
            {
              email: values.email,
              password: values.password,
            },
          );
          
          localStorage.setItem("accessToken", loginResponse.data.access);

          localStorage.setItem("refreshToken", loginResponse.data.refresh);

          localStorage.setItem("role", loginResponse.data.role);
          navigate("/student-profile");
        }
      } catch (err) {
        if (err.response?.status === 409) {
          setError(true);
        } else {
          console.log("Registration error:", err);
        }
      }
    },
  });

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Main Content */}
      <div className="w-full max-w-2xl mx-auto px-8 sm:px-10 pt-12 sm:pt-28">
        {/* Heading */}
        <div className="mb-10">
          <h1 className="text-4xl sm:text-6xl font-medium tracking-tight text-white">
            Student Register
          </h1>

          <p className="mt-3 text-lg sm:text-xl text-neutral-500">
            Already have an account?{" "}
            <Link
              to="/student-login"
              className="text-[#E85A24] hover:text-[#FF6B32] transition-colors"
            >
              Log in
            </Link>
          </p>
        </div>

        <form onSubmit={formik.handleSubmit}>
          {/* Email */}
          <div className="mb-7">
            <label
              htmlFor="email"
              className="block mb-3 text-lg text-neutral-300"
            >
              Email Address
            </label>

            <TextField
              id="email"
              name="email"
              type="email"
              fullWidth
              placeholder="Enter your email here"
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
                  padding: "12px",
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
          <div className="mb-6">
            <label
              htmlFor="password"
              className="block mb-3 text-lg text-neutral-300"
            >
              Password
            </label>

            <TextField
              id="password"
              name="password"
              fullWidth
              type={showPassword ? "text" : "password"}
              placeholder="Create a password"
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
                  padding: "12px",
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

          {/* Duplicate Email Error */}
          {error && (
            <div className="mb-5">
              <p className="text-red-500 text-sm">
                This email is already registered. Please log in.
              </p>
            </div>
          )}

          {/* Create Account Button */}
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
              Create Account
            </Button>
          </div>

          {/* Teacher Login */}
          <div className="flex justify-center">
            <Link
              to="/teacher-login"
              className="
              flex items-center justify-center
              w-full
              py-3
              rounded-xl
              border border-[#292929]
              text-neutral-300
              hover:border-[#E85A24]
              hover:text-white
              transition-all duration-300
            "
            >
              Login as a Teacher
            </Link>
          </div>
        </form>
      </div>

      {/* Footer */}
      <div className="mt-auto py-8">
        <p className="text-center text-sm text-neutral-600">
          Powered by Anshu & Mrinmoy
        </p>
      </div>
    </div>
  );
}
