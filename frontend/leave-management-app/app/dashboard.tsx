import { View, Text, Button, FlatList } from 'react-native';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function DashboardScreen() {
  const [leaveRequests, setLeaveRequests] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/leave-requests/')
      .then(response => {
        setLeaveRequests(response.data);
      })
      .catch(error => {
        console.error('Error fetching leave requests:', error);
      });
  }, []);

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 10 }}>
        Leave Requests
      </Text>
      <FlatList
        data={leaveRequests}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={{ padding: 10, borderBottomWidth: 1, borderBottomColor: '#ccc' }}>
            <Text>User ID: {item.user_id}</Text>
            <Text>Type: {item.leave_type}</Text>
            <Text>Start: {item.start_date}</Text>
            <Text>End: {item.end_date}</Text>
            <Text>Status: {item.status}</Text>
          </View>
        )}
      />
    </View>
  );
}
