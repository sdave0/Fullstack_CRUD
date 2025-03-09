// components/UserInterface.tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // Changed to default import from jwt-decode
import CardComponent from './CardComponent';
import { useRouter } from 'next/router';
import Image from 'next/image'; // Import Next.js Image component 

interface User {
  id: number;
  name: string;
  email: string;
  role?: string;
}

interface UserInterfaceProps {
  backendName: string;
}

const UserInterface: React.FC<UserInterfaceProps> = ({ backendName }) => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const [users, setUsers] = useState<User[]>([]);
  const [newUser, setNewUser] = useState({ name: '', email: '', password: '', role: 'user' });
  const [updateUser, setUpdateUser] = useState({ id: '', name: '', email: '' , role: 'user' });
  const [currentUserRole, setCurrentUserRole] = useState<string>('');
  const router = useRouter();

  const backgroundColors: { [key: string]: string } = {
    flask: 'from-blue-600 to-blue-400',
  };

  const buttonColors: { [key: string]: string } = {
    flask: 'bg-blue-600 hover:bg-blue-700',
  };

  const bgGradient = backgroundColors[backendName] || 'from-gray-600 to-gray-400';
  const btnColor = buttonColors[backendName] || 'bg-gray-600 hover:bg-gray-700';

  // Wrap handleLogout in useCallback so its identity is stable
  const handleLogout = useCallback(() => {
    localStorage.removeItem('token');
    router.push('/login');
  }, [router]);

  // Use useMemo to create the axios instance only when apiUrl changes
  const authAxios = useMemo(() => {
    const token = localStorage.getItem('token');
    return axios.create({
      baseURL: apiUrl,
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    });
  }, [apiUrl]);

  // Update useEffect to include handleLogout in dependency array
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.replace('/login');
      return;
    }
    try {
      const decoded: any = jwtDecode(token);
      setCurrentUserRole(decoded.role || '');
    } catch (error) {
      handleLogout();
    }
  }, [router, handleLogout]);

  // Include authAxios in dependency array
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await authAxios.get(`/api/${backendName}/users`);
        setUsers(response.data.reverse());
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, [backendName, authAxios]);

  const createUser = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      console.log('Sending user data:', newUser); // Optional: for debugging
      const response = await authAxios.post(`/api/${backendName}/users`, newUser);
      setUsers([response.data, ...users]);
      setNewUser({ name: '', email: '', password: '', role: 'user' });
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  const handleUpdateUser = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await authAxios.put(`/api/${backendName}/users/${updateUser.id}`, { 
        name: updateUser.name, 
        email: updateUser.email 
      });
      setUsers(users.map(user => 
        user.id === parseInt(updateUser.id) ? 
        { ...user, name: updateUser.name, email: updateUser.email } : 
        user
      ));
      setUpdateUser({ id: '', name: '', email: '', role: 'user' });
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  const deleteUser = async (userId: number) => {
    try {
      await authAxios.delete(`/api/${backendName}/users/${userId}`);
      setUsers(users.filter(user => user.id !== userId));
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const isAdmin = currentUserRole === 'admin';

  return (
    <div className={`min-h-screen bg-gradient-to-br ${bgGradient} py-8`}>
      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-8 p-6 bg-white rounded-lg shadow-xl">
          <div className="flex flex-col md:flex-row justify-between items-center mb-8">
            <div className="flex items-center mb-4 md:mb-0">
              <Image
                src={`/${backendName}logo.svg`}
                alt={`${backendName} Logo`}
                width={120}
                height={120}
                className="mr-4"
              />
              <h1 className="text-3xl font-bold text-gray-800">
                {`${backendName.charAt(0).toUpperCase() + backendName.slice(1)} Dashboard`}
              </h1>
            </div>
            <button 
              onClick={handleLogout}
              className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200"
            >
              Logout
            </button>
          </div>

          {isAdmin && (
            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <form onSubmit={createUser} className="p-6 bg-blue-50 rounded-xl shadow-md">
                <h3 className="text-xl font-semibold mb-4 text-blue-800">Create New User</h3>
                <input
                  placeholder="Name"
                  value={newUser.name}
                  onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                  className="mb-3 w-full p-2 border border-blue-200 rounded-md focus:ring-2 focus:ring-blue-500 text-black"
                  required
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  className="mb-3 w-full p-2 border border-blue-200 rounded-md focus:ring-2 focus:ring-blue-500 text-black"
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                  className="mb-4 w-full p-2 border border-blue-200 rounded-md focus:ring-2 focus:ring-blue-500 text-black"
                  required
                />
                {/* Checkbox for assigning admin role */}
                <div className="mb-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={newUser.role === 'admin'}
                      onChange={(e) =>
                        setNewUser({ ...newUser, role: e.target.checked ? 'admin' : 'user' })
                      }
                      className="mr-2"
                    />
                    <span className="text-blue-800">Assign Admin Role</span>
                  </label>
                </div>
                <button 
                  type="submit" 
                  className="w-full py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors duration-200"
                >
                  Add User
                </button>
              </form>

              <form onSubmit={handleUpdateUser} className="p-6 bg-green-50 rounded-xl shadow-md">
                <h3 className="text-xl font-semibold mb-4 text-green-800">Update Existing User</h3>
                <input
                  placeholder="User ID"
                  value={updateUser.id}
                  onChange={(e) => setUpdateUser({ ...updateUser, id: e.target.value })}
                  className="mb-3 w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-500 text-black"
                />
                <input
                  placeholder="Name"
                  value={updateUser.name}
                  onChange={(e) => setUpdateUser({ ...updateUser, name: e.target.value })}
                  className="mb-3 w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-500 text-black"
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={updateUser.email}
                  onChange={(e) => setUpdateUser({ ...updateUser, email: e.target.value })}
                  className="mb-4 w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-500 text-black"
                />
                <button 
                  type="submit" 
                  className="w-full py-2 text-white bg-green-600 rounded-md hover:bg-green-700 transition-colors duration-200"
                >
                  Update User
                </button>
              </form>
            </div>
          )}

          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">User List</h2>
            {users.map((user) => (
              <div 
                key={user.id} 
                className="flex flex-col md:flex-row items-center justify-between bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200"
              >
                <CardComponent card={user} />
                {isAdmin && (
                  <button 
                    onClick={() => deleteUser(user.id)} 
                    className={`mt-2 md:mt-0 ${btnColor} text-white py-2 px-6 rounded-md transition-colors duration-200`}
                  >
                    Delete
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserInterface;
