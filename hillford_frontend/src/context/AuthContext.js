import { createContext, useState, useEffect } from "react";
import jwt_decode from "jwt-decode";
import { useHistory } from "react-router-dom";
import { toast } from "react-toastify";


const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const history = useHistory();
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem("authTokens")
      ? jwt_decode(localStorage.getItem("authTokens"))
      : null
  );
  const [loading, setLoading] = useState(true);


  const loginUser = async (userData, errorData) => {
      try {
          const response = await fetch("http://127.0.0.1:8000/account/api/token/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify(userData)
            });
            const data = await response.json();
            if (response.status === 200) {
              setAuthTokens(data);
              setUser(jwt_decode(data.access));
              localStorage.setItem("authTokens", JSON.stringify(data));
              errorData.setLoading(false);
              history.push(`/account/user/dashboard`);
              toast.success("Login successful");
            } else {
              if (data.hasOwnProperty("detail")) {
                toast.error(data["detail"].toString())
              }
              if (data.hasOwnProperty("email")) {
                toast.error(`Email: ${data['email'].toString()}`, {position:'bottom-right'});
                errorData.setEmailError(data['email']);
              }
              if (data.hasOwnProperty("password")) {
                toast.error(`Password: ${data['password'].toString()}`, {position:'bottom-right'});
                errorData.setPasswordError(data['password']);
              }
              errorData.setLoading(false);
            };
      } catch (error) {
          toast.error(`Connection Error, try again later.`);
          errorData.setLoading(false);
      }
    
  };
  
  const registerUser = async (userData, errorData) => {
      try {
          const response = await fetch("http://127.0.0.1:8000/account/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(userData)
        });
        const data = await response.json();
        if (response.status === 201) {
          // history.push("/account/login");
          errorData.setLoading(false);
          toast.success(`Account for ${userData.email} created`);
          errorData.setVisible(true);
        } else {
          if (data.hasOwnProperty("detail")) {
            toast.error(data["detail"].toString());
          }
          if (data.hasOwnProperty("first_name")) {
            errorData.setFirstNameError(data["first_name"]);
          }
          if (data.hasOwnProperty("last_name")) {
            errorData.setLastNameError(data["last_name"]);
          }
          if (data.hasOwnProperty("other_name")) {
            errorData.setOtherNameError(data["other_name"]);
          }
          if (data.hasOwnProperty("email")) {
            errorData.setEmailError(data["email"]);
          }
          if (data.hasOwnProperty("telephone")) {
            errorData.setTelephoneError(data["telephone"]);
          }
          if (data.hasOwnProperty("address")) {
            errorData.setAddressError(data["address"]);
          }
          if (data.hasOwnProperty("city")) {
            errorData.setCityError(data["city"]);
          }
          if (data.hasOwnProperty("states")) {
            errorData.setStatesError(data["states"]);
          }
          if (data.hasOwnProperty("occupation")) {
            errorData.setOccupationError(data["occupation"]);
          }
          if (data.hasOwnProperty("date_of_birth")) {
            errorData.setDateOfBirthError(data["date_of_birth"]);
          }
          if (data.hasOwnProperty("password")) {
            errorData.setPasswordError(data["password"]);
          }
          if (data.hasOwnProperty("password2")) {
            errorData.setPassword2Error(data["password2"]);
          }
          errorData.setLoading(false);
        };
      } catch (error) {
          toast.error(`Connection Error, try again later.`);
          errorData.setLoading(false);
      }
    
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    toast.info("Logged out successful");
  };

  const contextData = {
    user,
    setUser,
    authTokens,
    setAuthTokens,
    registerUser,
    loginUser,
    logoutUser
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access));
    }
    setLoading(false);
  }, [authTokens, loading]);

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};