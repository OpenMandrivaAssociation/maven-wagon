%_javapackages_macros
%global bname     wagon

Name:           maven-%{bname}
Version:        2.5
Release:        2.1%{?dist}
Epoch:          0
Summary:        Tools to manage artifacts and deployment
License:        ASL 2.0
URL:            http://maven.apache.org/wagon
Source0:        http://repo1.maven.org/maven2/org/apache/maven/wagon/wagon/%{version}/wagon-%{version}-source-release.zip

Patch0:         0001-Port-to-jetty-9.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.jcraft:jsch)
BuildRequires:  mvn(commons-httpclient:commons-httpclient)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(commons-net:commons-net)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(log4j:log4j)
BuildRequires:  mvn(nekohtml:nekohtml)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.scm:maven-scm-api)
BuildRequires:  mvn(org.apache.maven:maven-parent)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interactivity-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.jetty:jetty-client)
BuildRequires:  mvn(org.eclipse.jetty:jetty-security)
BuildRequires:  mvn(org.eclipse.jetty:jetty-server)
BuildRequires:  mvn(org.eclipse.jetty:jetty-servlet)
BuildRequires:  mvn(org.eclipse.jetty:jetty-util)
BuildRequires:  mvn(org.jsoup:jsoup)
BuildRequires:  mvn(org.slf4j:slf4j-api)

Obsoletes:      %{name}-manual < %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-provider-test < %{epoch}:%{version}-%{release}

%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV
* SCM (in progress)

%package scm
Summary:        scm module for %{name}

%description scm
scm module for %{name}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n wagon-%{version}

%patch0 -p1

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_dep :wagon-tck-http wagon-providers/wagon-http

# correct groupId for jetty
%pom_xpath_set "pom:groupId[text()='org.mortbay.jetty']" "org.eclipse.jetty"

# disable tests, missing dependencies
%pom_disable_module wagon-tcks
%pom_disable_module wagon-ssh-common-test wagon-providers/pom.xml
%pom_disable_module wagon-provider-test

# missing dependencies
%pom_disable_module wagon-webdav-jackrabbit wagon-providers

%build
%mvn_file ":wagon-{*}" %{name}/@1

# scm module has a lot of dependencies
%mvn_package ":wagon-scm" scm

# tests are disabled because of missing dependencies
%mvn_build -f

# Maven requires Wagon HTTP with classifier "shaded"
%mvn_alias :wagon-http :::shaded:

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES
%files scm -f .mfiles-scm
%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE DEPENDENCIES

%changelog
* Mon Sep 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.5-2
- Add shaded alias for wagon-http

* Tue Sep 17 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.5-1
- Update to upstream version 2.5

* Thu Aug 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-3
- Disable unused wagon-provider-test module
- Resolves: rhbz#1002480

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Port to jetty 9

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Simplify build-requires

* Thu Feb 14 2013 Michal Srb <msrb@redhat.com> - 0:2.4-1
- Update to latest upstream 2.4
- Remove old depmap and patches
- Build with xmvn

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.0-7
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.0-6
- Remove BR: ganymed-ssh2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-4
- Fix build against jetty 8 and servlet 3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Jaromir Capik <jcapik@redhat.com> - 0:1.0-2
- Migration from plexus-maven-plugin to plexus-containers-component-metadata

* Wed Jul 27 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-1
- Update to 1.0 final.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.22
- Install wagon-providers depmap too.

* Tue Apr 26 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.3.b7.21
- Install wagon pom depmap.
- Use maven 3 for build.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b7.1
- Update to beta 7.
- Adapt to current guidelines.
- Fix pom names.

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b6.3
- Use javadoc:aggregate.
- Drop ant build.
- Use global instead of define.

* Fri May 14 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.2
- Create patch for wagon-http-shared pom.xml

* Wed May 12 2010 Yong Yang <yyang@redhat.com> 0:1.0-0.2.b6.1
- Update to beta 6, build with with_maven 1

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.7
- Remove gcj parts.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.2.b2.6
- Update to beta2 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.3.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.2.a5.3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0:1.0-0.1.a5.3.5
- include missing dir below _docdir

* Fri Oct 03 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3.4
- added patch to make it compatible with the newer version of jsch

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.1.a5.3.3
- drop repotag
- fix license tag

* Sat Apr 05 2008 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.2
- Rebuild with new version of jsch

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.0-0.1.a5.3jpp.1
- Merge in the changes neeeded to build without jetty
- Fix rpmlint issues
- Generate new *-build.xml files from pom.xml files as origins of
  *-project files is unknown.
- Remove maven1 project.xml files from sources
- Comment out various section requiring maven or javadocs
  (to be re-enabled at a future time). Note that the ant:ant task
  for maven2 does not currently generate javadocs.

* Tue Apr 04 2006 Ralph Apel <r.apel@r-apel.de> - 0:1.0-0.a5.3jpp
- Require j-c-codec, to build with j-c-httpclient = 3.0

* Thu Dec 22 2005 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.a5.2jpp
- Commented out potentially superfluous dependencies.
- Disabled wagon-scm

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.a5.1jpp
- First JPackage build
