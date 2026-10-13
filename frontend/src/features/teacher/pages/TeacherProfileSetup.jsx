import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useFormik } from "formik";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

import axios from "axios";

export default function TeacherProfileSetup() {
  const navigate = useNavigate();
  const [departments, setDepartments] = useState([]);
  const [error, setError] = useState("");

  const VITE_BASE_URL = import.meta.env.VITE_BASE_URL;
  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
    const fetchDepartment = async () => {
      try {
        // if (!accessToken) {
        //   navigate("/teacher-login", { replace: true });
        //   return;
        // }

        const response = await axios.get(
          `${VITE_BASE_URL}/api/departments/all/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        );

        if (response.status === 200) {
          setDepartments(response.data);
        }
      } catch (err) {
        if (err.response?.status === 401) {
          navigate("/teacher-login", { replace: true });
        }
      }
    };

    fetchDepartment();
  }, [navigate, VITE_BASE_URL, accessToken ]);

  const validate = (values) => {
    const errors = {};

    // Full Name validation
    if (!values.full_name.trim()) {
      errors.full_name = "Full name is required";
    } else if (values.full_name.trim().length < 4) {
      errors.full_name = "Full name must be greater than 4 characters";
    }

    // Department validation
    if (!values.department) {
      errors.department = "Department is required";
    }

    // Designation validation
    if (!values.designation.trim()) {
      errors.designation = "Designation is required";
    }

    // Profile picture is optional, but validate if provided
    if (values.profile_picture) {
      if (values.profile_picture.size > 15 * 1024 * 1024) {
        errors.profile_picture = "Image size must be less than 15 MB";
      }
    }
    return errors;
  };

  const formik = useFormik({
    initialValues: {
      full_name: "",
      profile_picture: "",
      department: "",
      designation: "",
      phone: "",
    },

    validate,

    onSubmit: async (values) => {
      setError("");
      console.log(values);

      const profileData = new FormData();

      profileData.append("full_name", values.full_name.trim());
      profileData.append("department", values.department);
      profileData.append("designation", values.designation.trim());
      profileData.append("phone", values.phone.trim());

      if (values.profile_picture instanceof File) {
        profileData.append("profile_picture", values.profile_picture);
      }

      try {
        if (!accessToken) {
          navigate("/teacher-login", { replace: true });
          return;
        }

        const finalProfileSetupResponse = await axios.patch(
          `${VITE_BASE_URL}/teacher_profile/`,
          profileData,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          },
        );

        console.log(finalProfileSetupResponse);

        if (finalProfileSetupResponse.status === 200) {
          navigate("/teacher/dashboard", { replace: true });
        }
      } catch (err) {
        const status = err.response?.status;
        if (status === 400) {
          setError("Please check the information you entered.");
        } else if (status === 401) {
          setError("Your session has expired. Please log in again.");
        } else if (status === 403) {
          setError("You do not have permission to update this profile.");
        }
      }
    },
  });

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <div className="w-full max-w-2xl mx-auto px-8 sm:px-10 pt-8 sm:pt-28">
        <div className="mb-6">
          <h1 className="text-3xl sm:text-6xl font-medium tracking-tight text-white">
            Complete your profile
          </h1>

          <p className="mt-4 text-lg sm:text-xl text-neutral-500">
            Go back to Log in?{" "}
            <Link
              to="/teacher-login"
              className="text-[#E85A24] hover:text-[#FF6B32] transition-colors"
            >
              Log in
            </Link>
          </p>
        </div>

        <form onSubmit={formik.handleSubmit}>
          <div className="mb-6">
            <label
              htmlFor="full_name"
              className="block mb-3 text-lg text-neutral-300"
            >
              Full Name <span className="text-[#E85A24]">*</span>
            </label>

            <TextField
              id="full_name"
              name="full_name"
              type="text"
              value={formik.values.full_name}
              onChange={(e) => {
                formik.handleChange(e);
                setError("");
              }}
              onBlur={formik.handleBlur}
              error={
                formik.touched.full_name && Boolean(formik.errors.full_name)
              }
              helperText={formik.touched.full_name && formik.errors.full_name}
              fullWidth
              placeholder="Enter your full name"
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
                    fontSize: "16px",
                  },
                },

                "& .MuiFormHelperText-root": {
                  marginLeft: 0,
                },
              }}
            />
          </div>
          <div className="mb-6">
            <FormControl fullWidth>
              <label
                htmlFor="department"
                className="block mb-3 text-lg text-neutral-300"
              >
                Department <span className="text-[#E85A24]">*</span>
              </label>

              <Select
                id="department"
                name="department"
                value={formik.values.department}
                onChange={(e) => {
                  formik.handleChange(e);
                  setError("");
                }}
                onBlur={formik.handleBlur}
                error={
                  formik.touched.department && Boolean(formik.errors.department)
                }
                fullWidth
                sx={{
                  height: "52px",
                  borderRadius: "12px",
                  backgroundColor: "#050505",
                  color: "#fff",
                  "& .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#292929",
                  },
                  "&:hover .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#444",
                  },
                  "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                    borderColor: "#E85A24",
                  },
                  "& .MuiSvgIcon-root": {
                    color: "#E85A24",
                  },
                }}
                MenuProps={{
                  PaperProps: {
                    sx: {
                      backgroundColor: "#141414",
                      color: "#fff",
                      "& .MuiMenuItem-root:hover": {
                        backgroundColor: "#292929",
                      },
                      "& .MuiMenuItem-root.Mui-selected": {
                        backgroundColor: "rgba(232, 90, 36, 0.18)",
                      },
                    },
                  },
                }}
              >
                <MenuItem value="" disabled>
                  Select your Department
                </MenuItem>

                {departments.map((dept) => (
                  <MenuItem key={dept.id} value={dept.id}>
                    {dept.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </div>
          <div className="mb-6">
            <label
              htmlFor="designation"
              className="block mb-3 text-lg text-neutral-300"
            >
              Designation <span className="text-[#E85A24]">*</span>
            </label>

            <TextField
              id="designation"
              name="designation"
              type="text"
              value={formik.values.designation}
              onChange={(e) => {
                formik.handleChange(e);
                setError("");
              }}
              onBlur={formik.handleBlur}
              error={
                formik.touched.designation && Boolean(formik.errors.designation)
              }
              helperText={
                formik.touched.designation && formik.errors.designation
              }
              fullWidth
              placeholder="Ex : Professor, Assistant Professor, Lecturer, etc."
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
                    fontSize: "14px",
                  },
                },

                "& .MuiFormHelperText-root": {
                  marginLeft: 0,
                },
              }}
            />
          </div>

          <div className="mb-6">
            <label
              htmlFor="phone"
              className="block mb-2 text-base text-neutral-300"
            >
              Phone Number
              <span className="ml-1 text-neutral-500">(Optional)</span>
            </label>

            <TextField
              id="phone"
              name="phone"
              type="tel"
              value={formik.values.phone}
              onChange={formik.handleChange}
              fullWidth
              placeholder="Enter a valid 10-digit phone number"
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
                    fontSize: "16px",
                  },
                },

                "& .MuiFormHelperText-root": {
                  marginLeft: 0,
                },
              }}
            />
          </div>

          <div className="mb-10">
            <label
              htmlFor="profile_picture"
              className="block mb-2 text-base text-neutral-300"
            >
              Profile Picture
              <span className="ml-1 text-neutral-500">(Optional)</span>
            </label>

            <input
              type="file"
              id="profile_picture"
              name="profile_picture"
              accept="image/*"
              onChange={(event) => {
                formik.setFieldValue(
                  "profile_picture",
                  event.currentTarget.files?.[0] || null,
                );
              }}
              onBlur={formik.handleBlur}
              className="w-full rounded-xl border border-[#292929] bg-[#101010] p-3 text-sm text-white
              file:mr-4 file:rounded-lg file:border-0
              file:bg-[#E85A24] file:px-4 file:py-2
              file:text-white file:font-medium file:cursor-pointer
              hover:file:bg-[#C94B1C]
              focus:outline-none focus:border-[#E85A24]"
            />
            {formik.touched.profile_picture &&
              formik.errors.profile_picture && (
                <p className="mt-2 text-sm text-red-500">
                  {formik.errors.profile_picture}
                </p>
              )}
          </div>

          {error && (
            <div className="mb-5">
              <p className="text-red-500 text-sm">{error}</p>
            </div>
          )}

          <div className="mb-8">
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={formik.isSubmitting}
              sx={{
                background: "linear-gradient(to right, #E85A24, #6b1b00)",
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
              {formik.isSubmitting ? "Saving profile..." : "Create Profile"}
            </Button>
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
