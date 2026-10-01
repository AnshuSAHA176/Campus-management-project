import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";
import raiganjUnivrsity from "../assets/Raiganj_univercity.png";

export default function LandingPage() {
  return (
    <div>
      <div
        className="bg-cover bg-center h-screen pt-15  flex justify-between flex-col w-full "
        style={{ backgroundImage: `url(${raiganjUnivrsity})` }}
      >
        <img className="w-45 ml-8" src={logo} alt="Raiganj_University" />
        <div className="bg-white py-6 px-6">
          <h2 className="text-2xl font-bold">Get Started with Classes </h2>
          <Link
            to="/student-login"
            variant="contained"
            color='success"'
            className="bg-[linear-gradient(to_right,#6844FC,#1B1464)]
            flex items-center justify-center w-full bg-black text-white py-2 rounded mt-6"
          >
            Continue
          </Link>
        </div>
      </div>
    </div>
  );
}
