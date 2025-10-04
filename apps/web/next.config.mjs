/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ["@dating/ui", "tamagui", "react-native", "react-native-web"],
  webpack: (config) => {
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      'react-native$': 'react-native-web',
    }
    return config
  }
};
export default nextConfig;
