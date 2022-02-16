var profileApp = angular.module('profileModule', []);

profileApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

profileApp.controller(
'profileController',
function($scope, $http, $timeout) {
	$scope.useHumanName = useHumanName;
	$scope.useDisplayName = useDisplayName;
	$scope.user = user;

	$scope.updateProfile = function(event) {
		event.preventDefault();
		var checkRegistrationData = {
			request: 'check-id',
			user: $scope.user,
		}
		$http.put('/user/profile/api/', checkRegistrationData).then(function(response){
			if(response.data.status != 'ok') {
				$scope.errors = response.data.errors;
			} else {
				$scope.showSuccess = true;
				$timeout(function() {
					$scope.showSuccess = false;
				}, 1500);
			}
		});
	}
	$scope.updatePassword = function(event) {
		event.preventDefault();
		var checkPasswordData = {
			request: 'update-password',
			current_password: $scope.currentPassword,
			new_password: $scope.newPassword,
		}
		$scope.passwordErrors = null;
		if($scope.currentPassword && $scope.newPassword) {
			if ($scope.newPassword != $scope.confirmPassword) {
				$scope.errors = ['Passwords must match', ];
			} else {
				$scope.errors = getPasswordErrors($scope.newPassword);
			}
			if (!$scope.errors.length){
				$http.put('/user/profile/api/', checkPasswordData).then(function(response){
					if(response.data.status != 'ok') {
						$scope.errors = response.data.errors;
					} else {
						window.location.replace("/user/login/");
					}
				});
			}
		}
	}

});

angular.bootstrap(document.getElementById("profileModule"), ['profileModule']);
