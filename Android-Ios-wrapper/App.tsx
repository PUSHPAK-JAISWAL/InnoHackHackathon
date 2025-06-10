import React from 'react';
import { SafeAreaView, StyleSheet, Platform } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  // Replace this with your IP address if accessing from a mobile device
  const localUrl = Platform.OS === 'android' ? 'http://192.168.103.84:8501' : 'http://localhost:8501';

  return (
    <SafeAreaView style={styles.container}>
      <WebView
        source={{ uri: localUrl }}
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  webview: {
    flex: 1,
  },
});
